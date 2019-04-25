const path = require('path'),
      MiniCssExtractPlugin = require('mini-css-extract-plugin');
      // CleanWebpackPlugin = require('clean-webpack-plugin');

module.exports = {
  entry: { main: './assets/js/app.js' },
  output: {
    path: path.resolve(__dirname, 'static'),
    filename: 'app.js'
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: {
          loader: "babel-loader"
        }
      },
      {
        test: /\.(sa|sc|c)ss$/,
        use:  [
          MiniCssExtractPlugin.loader,
          'css-loader',
          'postcss-loader',
          'sass-loader'
        ]
      },
      {
        test: /\.(otf|ttf|woff|woff2|svg|png|jpg)$/,
        use: [
          {
            loader: 'file-loader',
            options: {
              outputPath: 'assets'
            }
          },
        ],
      },
    ]
  },
  plugins: [
    // new CleanWebpackPlugin({
    //   cleanOnceBeforeBuildPatterns: ['**/*', '!src/**']
    // }),
    new MiniCssExtractPlugin({
      filename: 'app.css',
    })
  ]
};
