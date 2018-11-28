var webpack = require('webpack');

module.exports = {
  entry: './widget.js',
  output: {
    path: __dirname,
    filename: 'widget.dist.js'
  },
  module: {
    loaders: [
      {test: /\.css$/, loader: 'style!css'},
      {test: /\.svg|png$/, loader: 'url-loader'}
    ]
  },
  plugins: [
    // Handle missing file in web-design-standards
    new webpack.IgnorePlugin(/correct9\.png/)
  ]
};
