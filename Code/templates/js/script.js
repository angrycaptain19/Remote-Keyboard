/* Keywords */
const exit_string = "CodeEscape_Exit";
const exit_input = "Exit";
const keyboard = "keyboard.Key.";
const key_separator = '?';
const input = "input";
const go_string = "Go";

/* Keys */
const enter = 'enter';
const alt = 'alt';
const supr = 'delete';
const back = 'backspace';
const space = 'space';
const up = 'up';
const down = 'down';
const left = 'left';
const right = 'right';
const ctrl = 'ctrl';
const esc = 'esc';
const shft = 'shift';

const myFunc = keyword => {

    const ip = 'http://192.168.0.96:8000/';                                       
    let sender = ip;
    let x = new XMLHttpRequest();
    x.onreadystatechange = ()=>{
        if (x.readyState === 4 && x.status === 200)
            document.getElementById(input).value = ''
    };
    if (keyword === exit_input) sender += exit_string;
    else if (keyword === go_string) sender += document.getElementById(input).value;
    else{
        sender += keyboard + keyword + key_separator + document.getElementById(input).value;
    }

    x.open("GET", sender, true);
    x.send( null );
};