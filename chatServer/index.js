var app = require("express")()
var server = require("http").createServer(app)
var io = require("socket.io")(server,{
  pingTimeout: 1000,
})


app.all("/*", function(req, res, next) {
  res.header("Access-Control-Allow-Origin", "*")
  res.header("Access-Control-Allow-Headers", "X-Requested-With")
  next()
})

// localhost:3000서버에 접속하면 클라이언트로 메세지을 전송한다
app.get("/", function(req, res) {
  res.sendFile("Hellow Chating App Server")
})

io.sockets.on("connection", function(socket){
  // 연결되면 소켓 아이디를 콘솔에 출력

  // log 함수는 메세지를 클라이언트에 보내기 위한 함수임
  // socket emit으로 log 이벤트와 args로 'array'를 보냄

  // socket 이벤트인 'create or join' 이벤트에 대한 핸들러 추가
  socket.on("startMessage", data => {
    console.log("Received request to create or join room " + data.theme)
  
    // 'room'이름에 접속된 모든 소켓의 이름을 가져옴
    let clientsInRoom = io.sockets.adapter.rooms[data.theme]
    // 몇 개의 소켓이 접속되있는지 count
    let numClients = clientsInRoom ? Object.keys(clientsInRoom.sockets).length: 0
    console.log("Room " + data.theme + " now has " + numClients + " client(s)")

    // 연결된 소켓이 0이면, room에 참가하고, 'created' 이벤트 발생시킴
    if (numClients === 0) {
      socket.join(data.theme)
      console.log("Client ID " + socket.id + " created room " + data.theme)
      socket.emit("joined", {"theme": data.theme, nickname: "공지사항", message: data.theme + "방에 들어오셨습니다."})
    // 연결된 소켓이 1이면, 이미 존재하는 room에 참가하고, `joined` 이벤트 발생시킴
    } else {
      console.log("Client ID " + socket.id + " joined room " + data.theme)
      io.sockets.in(data.theme).emit("join", data.theme)
      socket.join(data.theme)
      socket.emit("joined", {"theme": data.theme, nickname: "공지사항", message: data.theme + "방에 들어오셨습니다."})
      io.sockets.in(data.theme).emit("ready")
    }
  })

  socket.on("sendMessage", data => {
    console.log(data)
    console.log(data.nickname + " send Meassage : " + data.message)
    socket.broadcast.to(data.theme).emit("message", data) // 나를 제외한 그룹 전체
  }) 
})

server.listen(3000, function() {
  console.log("socket io server listening on port 3000")
})