import axios from "axios"
const SERVER = "127.0.0.1:8000"
export default axios.create({
  baseURL: `http://${SERVER}/api`
})
