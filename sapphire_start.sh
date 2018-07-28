#/bin/bash

tmux new-session -d -s sapphire-backend

tmux split-window -t sapphire-backend:0 -h 
tmux split-window -t sapphire-backend:0 -h

tmux send-keys -t sapphire-backend:0.0 'feed.sh' Enter
tmux send-keys -t sapphire-backend:0.1 'content.sh' Enter
tmux send-keys -t sapphire-backend:0.2 'util.sh' Enter

tmux new-window -t sapphire-backend:1 -n console

tmux send-keys -t sapphire-backend:1 'console.sh' Enter

tmux a -t sapphire-backend:0
