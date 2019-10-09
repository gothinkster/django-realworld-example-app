## Onboarding (5 minutes)

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
    5. Launch the URL and hit “/api/artilces”…No articles
    6. The breakpoint will be hit
    7. Step the debugger, see the issue and then correct it
    8. Change line 30 to “if author is not None:” and then re-run the app. You’ll now see the article data returned
4. “It’s just like developing with VS Code, but without any of the setup, and accessible from anywhere”
    1. If I need to open it in desktop, I can (seamless interop, so you can choose how to work)
        1. Show the change on line 30 in articles/views.py
    2. When I’m done, I can shut it down, or let it automatically go to sleep

> Dev starts to make their intended change, and is assisted along the way by IntelliCode…

## AI-assistance (3 minutes)

1. Completion suggestions
2. Whole line completion
3. Refactorings
4. PR

> Dev wants to get some early feedback on their change, so they invite their mentor into an LS session…

## Real-time Collaboration (3 minutes) -  “Full-fidelity Live Share works in the browser”

1. Direct invite (via Contacts pane)
2. Chat (via the LS Chat extension being installed)
3. Inline code comments (doing a lightweight code review)
4. Guest IntelliCode (Optional)
5. Debugging/Port forwarding (Optional) - “These work, despite the fact that the host is actually running in the cloud!”
