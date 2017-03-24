<template>
    <div class="container-fluid">
        <div class="row">
            <nav class="col-sm-3 col-md-2 sidebar bg-faded">
                <ul class="nav flex-column">
                    <li class="nav-item">
                        <router-link class="nav-link active" to="/crt-manager/machine-list">我的主机</router-link>
                    </li>
                    <li class="nav-item">
                        <router-link class="nav-link" to="/crt-manager/add-remove">添加主机</router-link>
                    </li>
                    <li class="nav-item">
                        <router-link class="nav-link" to="/crt-manager/password">管理主机密码</router-link>
                    </li>
                </ul>
            </nav>
        </div>
        <div class="main-view">
            <div id="terminal-container"></div>
        </div>
    </div>
    
</template>

<script>
import Bus from '../bus.js';
import Terminal from 'xterm'
import '../attach.js'
import 'xterm/dist/xterm.css';

export default {
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

<style>
.main-view{
    margin-left:35%;
}

.sidebar {
    padding-left: 0;
    padding-right: 0;
    position: fixed;
    top: 51px;
    bottom: 0;
    left: 0;
    z-index: 1000;
    padding: 20px;
    overflow-x: hidden;
    overflow-y: auto;
    border-right: 1px solid #eee;
}

.bg-faded {
    background-color: #f7f7f7;
}
</style>