# chat

가져가실 때
fornt에서
npm install socket.io-client

main.js에서
import io from 'socket.io-client';
const socket = io('');
Vue.prototype.$socket = socket;


사용시
handler는 방을 만들고
sendMessage는 메시지를 보냅니다.
created는 socket에서 온 메시지를 실시간으로 받습니다.

