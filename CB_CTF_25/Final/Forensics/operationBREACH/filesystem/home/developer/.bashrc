# Developer User Bash Configuration
# ~/.bashrc: executed by bash for non-login shells.

# If not running interactively, don't do anything
case $- in
    *i*) ;;
      *) return;;
esac

# Set prompt
PS1='\u@\h:\w\$ '

# Aliases
alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'
alias grep='grep --color=auto'

# Development aliases
alias php='php -d display_errors=1'
alias mysql='mysql -u root -p'
alias git-status='git status --porcelain'

# Project directory
export PROJECT_DIR=/var/www/html 