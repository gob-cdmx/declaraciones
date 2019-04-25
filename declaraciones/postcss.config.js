module.exports = {
    plugins: [
      require('autoprefixer') ({
          grid: 'autoplace',
          flexbox: 'no-2009'
      }),
      require('css-mqpacker'),
      require('cssnano')
    ]
}