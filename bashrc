alias mk="~/scripts/./make_default.sh && cd build"
alias mkt="~/scripts/./make_tests.sh && cd build"
alias fuck='eval $(thefuck $(fc -ln -1)); history -r'
tput cup $(tput lines) 0
force_color_prompt=yes

export EDITOR='vim'
export VISUAL='vim'
export CC=/usr/bin/clang
export CXX=/usr/bin/clang++

