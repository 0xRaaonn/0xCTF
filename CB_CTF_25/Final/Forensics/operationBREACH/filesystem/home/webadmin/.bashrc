# WebAdmin User Bash Configuration
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

# Web server management aliases
alias restart-apache='sudo systemctl restart apache2'
alias restart-nginx='sudo systemctl restart nginx'
alias check-logs='tail -f /var/log/apache2/access.log' 