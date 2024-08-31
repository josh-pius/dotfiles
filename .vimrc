"      _                    
"__   _(_)_ __ ___  _ __ ___ 
"\ \ / / | '_ ` _ \| '__/ __|
" \ V /| | | | | | | | | (__ 
"(_)_/ |_|_| |_| |_|_|  \___|
                            
" Map jk to escape
inoremap jk <Esc>
" Deactivate line numbers
set nonumber

" ################# Tabs and Spaces #################
" number of spaces to replace a tab with when expandtab
set tabstop=4
" Replace spaces with tabs
set expandtab
set softtabstop=4
set shiftwidth=4
set autoindent

" ################################################## 


" ################# Misc #################

" Disable bell (also disable in .inputrc)
set noerrorbells
set vb t_vb=


" turn col and row position on in bottom right
set ruler " see ruf for formatting

" prevents truncated yanks, deletes, etc.
set viminfo='20,<1000,s1000

" Python Specific Formatting Options
autocmd FileType python setlocal expandtab
autocmd FileType python setlocal tabstop=4
autocmd FileType python setlocal shiftwidth=4
autocmd FileType python setlocal softtabstop=4


" Autosave Racket Files
autocmd TextChanged,TextChangedI *.rkt if &modified | silent! write | endif


" Paste from windows clipboard
nnoremap <space>p :.!powershell.exe -c "Get-Clipboard"<CR>

" stop complaints about switching buffer with changes
set hidden

" Turn on syntax highlighting
syntax on
" Highlight cursor line
" set cursorline
" :highlight CursorLine ctermbg=grey

" ################ Set tabstop, softtabstop and shiftwidth to the same value ################
" http://vimcasts.org/episodes/tabs-and-spaces/


command! -nargs=* Stab call Stab()
function! Stab()
    let l:tabstop = 1 * input('set tabstop = softtabstop = shiftwidth = ')
    if l:tabstop > 0
        let &l:sts = l:tabstop
        let &l:ts = l:tabstop
        let &l:sw = l:tabstop
    endif
    call SummarizeTabs()
    endfunction

function! SummarizeTabs()
    try
        echohl ModeMsg
        echon 'tabstop='.&l:ts
        echon ' shiftwidth='.&l:sw
        echon ' softtabstop='.&l:sts
        if &l:et
            echon ' expandtab'
        else
            echon ' noexpandtab'
        endif
        finally
            echohl None
    endtry
endfunction

" ################################################################################## 
