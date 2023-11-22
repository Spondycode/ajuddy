============================================
# pass: the standard unix password manager 
             Jason A. Donenfeld           
               Jason@zx2c4.com            
      http://www.passwordstore.org/       
============================================

## Usage:

*       pass init [--path=subfolder,-p subfolder] gpg-id...
        Initialize new password storage and use gpg-id for encryption.
        Selectively reencrypt existing passwords using new gpg-id.

*     pass [ls] [subfolder]
        List passwords.

*     pass find pass-names...
        List passwords that match pass-names.

*     pass [show] [--clip[=line-number],-c[line-number]] pass-name
        Show existing password and optionally put it on the clipboard.
        If put on the clipboard, it will be cleared in 45 seconds.

*     pass grep [GREPOPTIONS] search-string
        Search for password files containing search-string when decrypted.

*     pass insert [--echo,-e | --multiline,-m] [--force,-f] pass-name
        Insert new password. Optionally, echo the password back to the console
        during entry. Or, optionally, the entry may be multiline. Prompt before
        overwriting existing password unless forced.

*     pass edit pass-name
        Insert a new password or edit an existing password using vi.

*     pass generate [--no-symbols,-n] [--clip,-c] [--in-place,-i | --force,-f] pass-name [pass-length]
        Generate a new password of pass-length (or 25 if unspecified) with optionally no symbols.
        Optionally put it on the clipboard and clear board after 45 seconds.
        Prompt before overwriting existing password unless forced.
        Optionally replace only the first line of an existing file with a new password.

*     pass rm [--recursive,-r] [--force,-f] pass-name
        Remove existing password or directory, optionally forcefully.

*     pass mv [--force,-f] old-path new-path
        Renames or moves old-path to new-path, optionally forcefully, selectively reencrypting.

*     pass cp [--force,-f] old-path new-path
        Copies old-path to new-path, optionally forcefully, selectively reencrypting.

*     pass git git-command-args...
        If the password store is a git repository, execute a git command
        specified by git-command-args.

*     pass help
        Show this text.

*     pass version
        Show version information.

More information may be found in the pass(1) man page.
