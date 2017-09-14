# Git settings 

## git init and basic user settings 

```bash
$ git init 
$ git config --global user.name "your name"
$ git config --global user.email "your email"

```

## git basic add

```bash
$ git add <filename1> <filename2>    # also can be `git add .` or `git add *` or `git add -A`
$ git commit <filename1> <filename2> -m "commit descriptions" # filename can be changed as above

```

## version reset

- if you changed file and have not `git add` file, and you wanna get it back

```bash
$ git checkout -- <filename>

```

- if you have changed and `git add`, then you have to 

```bash
$ git reset HEAD <filename>

```

### all file change

- use `git reset --hard <commit_id>` to change all files to the specify version

- use `git log` to show all the commit history, and find the commit_id

- if you are reset to old commit and wanna get back, use `git reflog` to show command history, and change the version to the future.