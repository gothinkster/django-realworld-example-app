from __future__ import unicode_literals

from django.shortcuts import render, redirect


from account.decorators import login_required


@login_required
def dashboard(request):
    if request.session.get("pending-token"):
        return redirect("speaker_create_token",
                        request.session["pending-token"])
    return render(request, "dashboard.html")
