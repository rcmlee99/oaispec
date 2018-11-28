'use strict';

/* global window, document, require */

var $ = require('jquery');
var template = require('html!./template.html');
require('web-design-standards/css/main.css');

var css = {
  'text-align': 'center',
  position: 'fixed',
  bottom: 0,
  right: 0
};

function FeedbackWidget(url, target) {
  this.url = url;
  this.target = target;
  $(document).ready(this.init.bind(this));
}

FeedbackWidget.prototype.init = function () {
  var $form = $(template).css(css);
  $form.appendTo(this.target || document.body);
  $form.on('click', 'button[value]', this.handleClick.bind(this));
};

FeedbackWidget.prototype.handleClick = function(e) {
  var value = $(e.target).val();
  this.submit(value);
};

FeedbackWidget.prototype.submit = function(upvote) {
  var data = {
    url: window.location.href,
    referer: document.referrer || null,
    upvote: upvote
  };

  var promise = $.ajax({
    method: 'POST',
    url: this.url,
    data: JSON.stringify(data),
    contentType: 'application/json'
  });
  promise.done(this.handleSuccess.bind(this));
  promise.fail(this.handleError.bind(this));
};

FeedbackWidget.prototype.handleSuccess = function(response) {
  console.log('Submitted feedback');
};

FeedbackWidget.prototype.handleError = function() {
  console.log('Error submitting feedback');
};

window.FeedbackWidget = FeedbackWidget;
