from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Party, Vote


def dashboard(request):
    total_votes = Vote.objects.count()
    parties = Party.objects.all()
    has_voted = False
    voted_party = None

    if request.user.is_authenticated:
        try:
            vote = Vote.objects.get(user=request.user)
            has_voted = True
            voted_party = vote.party
        except Vote.DoesNotExist:
            pass
    return render(request, 'voting/dashboard.html', {
        'total_votes': total_votes,
        'parties': parties,
        'has_voted': has_voted,
        'voted_party': voted_party,
    })


@login_required
@check_honeypot
def vote(request):
    try:
        existing = Vote.objects.get(user=request.user)
        messages.warning(request, f'You have already voted for {existing.party.name}.')
        return redirect('dashboard')
    except Vote.DoesNotExist:
        pass

    if request.method == 'POST':
        party_id = request.POST.get('party_id')

        try:
            party = Party.objects.get(id=party_id)
            Vote.objects.create(user=request.user, party=party)
            messages.success(request, f'✅Vote cast successfully for {party.name}!')
            return redirect('results')
        except Party.DoesNotExist:
            messages.error(request, 'Invalid party selected.')
        
    parties = Party.objects.all()
    return render(request, 'voting/vote.html', {'parties': parties})



def results(request):
    parties = Party.objects.all()
    total_votes = Vote.objects.count()
    results_data = []
    leading_party = None
    max_votes = 0
    for party in parties:
        count = party.vote_count()
        pct = round((count / total_votes * 100), 1) if total_votes > 0 else 0
        results_data.append({'party': party, 'count': count, 'percentage': pct})
        if count > max_votes:
            max_votes = count
            leading_party = party
    return render(request, 'voting/results.html', {
        'results_data': results_data,
        'total_votes': total_votes,
        'leading_party': leading_party,
    })

def results_api(request):
    parties = Party.objects.all()
    total = Vote.objects.count()
    data = []
    for p in parties:
        c = p.vote_count()
        data.append({
            'name': p.name,
            'bengali_name': p.bengali_name,
            'symbol': p.symbol,
            'color': p.color,
            'votes': c,
            'percentage': round(c / total * 100, 1) if total > 0 else 0,
        })
    return JsonResponse({'parties': data, 'total': total})

