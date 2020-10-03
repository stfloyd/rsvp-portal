import axios from 'axios'

const ApiService = {
  init(baseURL: string) {
    axios.defaults.baseURL = baseURL
    axios.defaults.xsrfCookieName = 'csrftoken'
    axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN'
    axios.interceptors.response.use(
      function(response) {
        return response
      },
      function(error) {
        return Promise.reject(error)
      }
    )
  },

  get(resource: string) {
    return axios.get(resource)
  },

  post(resource: string, data: object) {
    return axios.post(resource, data)
  },

  put(resource: string, data: object) {
    return axios.put(resource, data)
  },

  delete(resource: string) {
    return axios.delete(resource)
  },

  /**
   * Perform a custom Axios request.
   *
   * data is an object containing the following properties:
   *  - method
   *  - url
   *  - data ... request payload
   *  - auth (optional)
   *    - username
   *    - password
   **/
  request(data: object) {
    return axios(data)
  }
}

ApiService.init('/api')

export default ApiService
