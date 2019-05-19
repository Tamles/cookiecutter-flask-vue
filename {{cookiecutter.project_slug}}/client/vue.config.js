const port = 5000

module.exports = {
  devServer: {
    proxy: {
      [process.env.VUE_APP_BASE_API]: {
        target: `http://localhost:${port}`,
        changeOrigin: true
      }
    }
  }
}
