#!/bin/bash
# Git post-commit hook for optional manual deployment trigger
# Copy this to .git/hooks/post-commit and make it executable

echo "🚀 Bytecode Interpreter - Post-commit hook"

# Check if we're on the main branch
current_branch=$(git rev-parse --abbrev-ref HEAD)

if [ "$current_branch" = "main" ] || [ "$current_branch" = "master" ]; then
    echo "📋 Committed to $current_branch branch"
    echo "🔄 GitHub Actions will automatically deploy this commit"
    echo "📊 View deployment progress at: https://github.com/$(git config --get remote.origin.url | sed 's/.*github.com[:/]\([^.]*\).*/\1/')/actions"
    
    # Optional: Add manual deployment command
    # Uncomment the following lines if you want to deploy immediately
    # echo "🔧 Would you like to deploy manually now? (y/N)"
    # read -r response
    # if [ "$response" = "y" ] || [ "$response" = "Y" ]; then
    #     echo "🚀 Deploying to Fly.io..."
    #     flyctl deploy
    # fi
else
    echo "📋 Not on main branch ($current_branch), no automatic deployment"
fi

echo "✅ Post-commit hook complete"
