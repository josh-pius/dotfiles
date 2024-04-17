inoremap jk <Esc>
set rnu
set nu
set tabstop=3


### Autosave Racket Files
autocmd TextChanged,TextChangedI *.rkt if &modified | silent! write | endif




