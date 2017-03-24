<template>
    <div id="terminal"></div>
</template>

<script>
import Bus from '../bus.js';

expoort default {
    data: {
        term: new Terminal({ cursorBlink: true }),
        socket: new WebSocket("ws://127.0.0.1:8888/shell?username=");
    },

    created: function(){
        this.createTerminal()
        Bus.$on('xtermChange', (id) => {
            this.socket.close()
            this.socket = new WebSocket("ws://127.0.0.1:8888/shell?username=" + id);
            this.createTerminal();
        })
    },

    methods: {
        createTerminal: function(){
            // this.socket = new WebSocket("ws://127.0.0.1:8888/shell?username=" + id);
            this.term.open(document.getElementById('#terminal'));
            this.term.writeln('Hello world ');
            this.term.fit();
    
            this.socket.onopen = runRealTerminal;
            this.socket.onclose = runFakeTerminal;
            this.socket.onerror = runFakeTerminal;
        }

        runRealTerminal: function(){
            this.term.attach(this.socket);
            this.term._initialized = true;
        },

        runFakeTerminal: function(){
            if (this.term._initialized) {
                return;
            }

            this.term._initialized = true;

            let shellprompt = '$ ';

            this.term.prompt = function() {
                this.term.write('\r\n' + shellprompt);
            };

            this.term.writeln('Welcome to MyCRT');
            this.term.writeln('This is a local terminal emulation, without a real terminal in the back-end.');
            this.term.writeln('Type some keys and commands to play around.');
            this.term.writeln('');
            this.term.prompt();

            this.term.on('key', function(key, ev) {
                let printable = (!ev.altKey && !ev.altGraphKey && !ev.ctrlKey && !ev.metaKey);

                if (ev.keyCode == 13) {
                    this.term.prompt();
                } else if (ev.keyCode == 8) {
                    // Do not delete the prompt
                    if (this.term.x > 2) {
                        this.term.write('\b \b');
                    }
                } else if (printable) {
                    this.term.write(key);
                }
            });s

            this.term.on('paste', function(data, ev) {
                this.term.write(data);
            });
        }
    }
}
</script>