_linchpin_completion() {
    COMPREPLY=( $( env COMP_WORDS="${COMP_WORDS[*]}" \
                   COMP_CWORD=$COMP_CWORD \
                   _LINCHPIN_COMPLETE=complete $1 ) )
    return 0
}

complete -F _linchpin_completion -o default linchpin;
