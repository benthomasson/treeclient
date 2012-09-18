
set nocompatible
:set tabstop=4 
:set expandtab 
:set shiftwidth=4 
:set hi=1000 
:set smartindent 
:set ul=1000
:set nu
:set ai
:set backspace=2
:set hls
:set incsearch
:set hlsearch
:set ruler
:set showmatch
:syntax on
:let g:html_tag_case = 'lowercase'
:let python_highlight_all = 1
:set pastetoggle=<F2>


" Auto-completion search
:set complete=.,b,w,u,t

:filetype on
":filetype ident on
:filetype plugin on

:set vb t_vb=


let Tlist_Ctags_Cmd = "/usr/local/bin/ctags"
let Tlist_WinWidth = 50

:map gf :e <cfile><CR>

nnoremap <silent><C-T> :po<CR>

"set spellfile=~/.vim/spellfile.add
:set foldmethod=indent 
"source ~/xoria256.vim

"For Python
"set term=builtin_ansi
"syntax on
autocmd BufRead *.py set smartindent cinwords=if,elif,else,for,while,try,except,finally,def,class
autocmd BufRead *.py highlight BadWhitespace ctermbg=red guibg=red

nnoremap <silent><C-n> :tabnext<CR><CR>
nnoremap <silent><C-p> :tabprevious<CR><CR>

set wildmenu
set wildmode=list:longest
let mapleader = ","
set hidden
set title
set backspace=indent,eol,start
set nobackup
set nowritebackup
set noswapfile

map <F3> <Esc>:w<CR>:!%:p<CR>


:highlight Comment ctermfg=white
:highlight Folded ctermbg=white
:set tags=./tags;
command Ptags :! find -X . -name \*.py -print | xargs ptags.py
