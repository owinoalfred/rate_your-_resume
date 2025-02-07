# auto_push.ps1
# Add all changes
git add .

# Get the list of changed files
$changes = git diff --cached --name-only

if (-not $changes) {
    Write-Output "No changes to commit."
} else {
    # Create a meaningful commit message
    $commitMsg = "Updated: $($changes -join ', ')"
    Write-Output "Committing changes with message: $commitMsg"

    # Commit and push
    git commit -m $commitMsg
    git push
}
