@    ;
{3};3 tags
{3};tag length 1(4 bytes)
@scheduler   ;tag for name
{1};tag length 1(4 bytes)
@.exe;tag for file type
{3};tag length 3(12 bytes)
@immutable   ;tag, comment used for proper parsing

>bootup_label

;startup and load the terminal :3

>main_loop_label



;find a process, allocate a core to it, then spin if no process is availiable





<main_loop_label
jmp

