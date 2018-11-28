# Feedback widget

This was a quick experiment in prototyping a simple website feedback form ("How was your experience? [Good / Bad]"). See [this repository's issues](https://github.com/18F/feedback-widget/issues) for some discussion of this idea and a few examples of feedback widgets on government websites (including issues [#2](https://github.com/18F/feedback-widget/issues/2) and [#6](https://github.com/18F/feedback-widget/issues/6)). We're not planning to continue working on this particular prototype, but you're welcome to learn from what we've posted!

## Usage

To add to your site, add the following to your `<head>`:

```html
<script src="widget.js"></script>
<script>
  new FeedbackWidget(url);
</script>
```

You can optionally pass in a target element where you want the widget to be added:

```javascript
var element = document.getElementById('...'); // or whatever
new FeedbackWidget.init(url, element);
```

## Development

### API

This repository also includes an API for collecting the data.

1. Install the dependencies.
    * Python
    * PostgreSQL
1. Run:

    ```bash
    pip install -r requirements.txt
    python app.py
    ```

### Widget

1. Make changes to [`widget.js`](widget.js).
1. Install the dependencies.
    * Node
1. Run:

    ```bash
    npm run build
    ```

The new build will be placed in `widget.dist.js`. Open `index.html` in your browser to test it.
