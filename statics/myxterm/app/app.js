import Terminal from 'xterm';
require("./attach.js")
import 'xterm/dist/xterm.css';

let term = new Terminal({ cursorBlink: true });
term.open(document.getElementById('#terminal'));
term.writeln('Hello world ')

let socket = new WebSocket("ws://127.0.0.1:8888/shell")
socket.onopen = runRealTerminal;
socket.onclose = runFakeTerminal;
socket.onerror = runFakeTerminal;


function runRealTerminal() {
    term.attach(socket);
    term._initialized = true;
}

function runFakeTerminal() {
    if (term._initialized) {
        return;
    }

    term._initialized = true;

    let shellprompt = '$ ';

    term.prompt = function() {
        term.write('\r\n' + shellprompt);
    };

    term.writeln('Welcome to MyCRT');
    term.writeln('This is a local terminal emulation, without a real terminal in the back-end.');
    term.writeln('Type some keys and commands to play around.');
    term.writeln('');
    term.prompt();

    term.on('key', function(key, ev) {
        let printable = (!ev.altKey && !ev.altGraphKey && !ev.ctrlKey && !ev.metaKey);

        if (ev.keyCode == 13) {
            term.prompt();
        } else if (ev.keyCode == 8) {
            // Do not delete the prompt
            if (term.x > 2) {
                term.write('\b \b');
            }
        } else if (printable) {
            term.write(key);
        }
    });

    term.on('paste', function(data, ev) {
        term.write(data);
    });
}