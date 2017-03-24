<template>
    <div id="terminal-container"></div>
</template>

<script>
import Bus from '../bus.js';
import Terminal from 'xterm'
import '../attach.js'
import 'xterm/dist/xterm.css';

export default {
    // data: {
    //     term: new Terminal({ cursorBlink: true }),
    //     socket: new WebSocket("ws://127.0.0.1:8888/shell"),
    // },
    data: function(){
        return {
            term: new Terminal({ cursorBlink: true }),
            socket: new WebSocket("ws://127.0.0.1:8888/shell"),
        }
    },

    created: function(){
        Bus.$on('xtermChange', (id) => {
            this.socket.close()
            this.socket = new WebSocket("ws://127.0.0.1:8888/shell?username=" + id);
            this.createTerminal();
        })
    },

    mounted:function(){
        this.createTerminal()
    },

    destroyed:function(){
        this.socket.close()
    },

    methods: {
        createTerminal: function(){
            // this.socket = new WebSocket("ws://127.0.0.1:8888/shell?username=" + id);
            this.term.open(document.getElementById('terminal-container'));
            console.log(document.getElementById('terminal-container'));
    
            this.socket.onopen = this.runRealTerminal;
            this.socket.onclose = this.runFakeTerminal;
            this.socket.onerror = this.runFakeTerminal;
        },

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
            });

            this.term.on('paste', function(data, ev) {
                this.term.write(data);
            });
        }
    }
}
</script>