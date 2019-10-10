## Setup

1. Install the [JSON Formatter extension](https://chrome.google.com/webstore/detail/json-formatter/bcjindcccaagfpapjjmafapmmgkkhgoa?hl=en) for Chrome
1. Ensure you've already authenticated with VSO + GitHub once, so that you can push changes during the demo, without needing to auth
1. Ensure that you've opened up the `conduit/apps/articles/views.py` file once, and leave it open, so that VSO will default it to be open for you when you create a new environment

## Onboarding 

1. Developer sees an [issue on GitHub](https://github.com/lostintangent/Conduit/issues/1) and clicks a link to deep link into an instance. The issue mentions that the REST API no longer returns articles, even though they're in the database - [Create VSO Environment](https://online-ppe.core.vsengsaas.visualstudio.com/environments/new?name=Conduit&repo=https://github.com/lostintangent/Conduit)
    1. Show that they don’t have Python installed on their local machine
1. They create the environment and are taken into the web editor, with…
    1. The repo automatically cloned
    2. Their Python dependencies installed (Python/PIP are now available in the terminal) - Run “python —version” from the terminal
    3. Their extensions automatically installed (the Python extension) - Switch to the extensions tab and show it (May need to reload)
    4. The app automatically built (PIP install was run) - Show the VSO terminal instance
    5. Their dot files automatically roamed (shell aliases are available) - Run the “party” command
2. Full fidelity tools
    1. File access/Search
    2. Extensions (show GitLens?)
    3. Terminals (run a command such as “ls”)
3. Debugging/Port forwarding
    1. Set a breakpoint on line 30 of articles/views.py
    2. Hit F5, then select “Python: Django"
    3. CTRL+Click the URL in the terminal
    5. Launch the URL and hit “/api/articles”…No articles (!)
    6. The breakpoint will be hit
    7. Step the debugger, see the issue and then correct it
    8. Change line 30 to “if author is not None:” and then re-run the app. You’ll now see the article data returned
    9. Remove the breakpoint on line 30, hit the debug refresh button, and refresh the browser window to show the article data correctly being returned
4. Git operations
    1. Commit the changes you made and highlight that you're Git identity was roamed
    1. Push the changes back to the remote, to highlight you automatically have permissions to the repo
4. “It’s just like developing with VS Code, but without any of the setup, and accessible from anywhere”
    1. If I need to open it in desktop, I can (seamless interop, so you can choose how to work)
        1. Show the change on line 30 in articles/views.py
    2. When I’m done, I can shut it down, or let it automatically go to sleep

> Dev starts to make their intended change, and is assisted along the way by IntelliCode…

## AI-assistance 

1. Whole line completion
    1. Add the following code to the bottom of the `symposion/reviews/forms.py` file
    
        ```python
        Class StaffRequestForm(forms.Form):
	    	staffIDs = forms.CharField(label=_(“Command separated list of IDs”, max_length=5000)
        ```
        
    1. Add the following to the bottom of the `symposion/reviews/views.py` file (within the last function's `if` statement)
    
        ```python
        if form.is_valid():
		staff_ids = form.cleaned_data.get(“staff_ids”).split(“,”)
		for staff_ids in staff_ids:
			accept_staff_suggestion(staff_ids)
        ```
        
2. Refactorings (still in `views.py`)
    1. Replace a call to `render` with a call to `access_not_permitted'
    1. Replace a second instance
    1. Notice that IntelliCode has detected the repeated edits and is suggesting other locations
    1. Click one of the suggestions in the `Problems` pane and accept it
    1. Select another one, but this time, choose to have IntelliCode submit a PR on your behalf (!)
    1. When the PR page is launched, highlight that it took care of all of the refactorings, and allowed you to keep your changes focused

> Dev wants to get some early feedback on their change, so they invite their mentor into an LS session…

## Real-time Collaboration 

1. Direct invite (via Contacts pane)
2. Chat (via the LS Chat extension being installed)
3. Inline code comments (doing a lightweight code review)
4. Guest IntelliCode (Optional)
5. Debugging/Port forwarding (Optional) - “These work, despite the fact that the host is actually running in the cloud!”
