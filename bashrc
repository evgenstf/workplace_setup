alias mk="~/scripts/./make_default.sh && cd build"
alias mkt="~/scripts/./make_tests.sh && cd build"
alias fuck='eval $(thefuck $(fc -ln -1)); history -r'
alias mux=tmuxinator

tput cup $(tput lines) 0
force_color_prompt=yes

export EDITOR='vim'
export VISUAL='vim'
export CC=/usr/bin/clang
export CXX=/usr/bin/clang++

mux start dev
HISTTIMEFORMAT="%d/%m/%y %T "

export PATH=/usr/local/clang_9.0.0/bin:$PATH
export LD_LIBRARY_PATH=/usr/local/clang_9.0.0/lib:$LD_LIBRARY_PATH
