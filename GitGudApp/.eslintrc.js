const path = require('path');

module.exports = {
  extends: 'eslint-config-react-app',
  settings: {
    'import/resolver': {
      node: {
        paths: [path.resolve(__dirname, './src')]
      }
    }
  },
  rules: {
    'no-console': ['warn', { allow: ['warn', 'error'] }],
    //We are wanting to do stuff like `<a onClick={this.whatever}>Click me</a>`
    //and it was wanting us to put an href on it since it was an anchor. I (ks) forget
    //about the a11y rule, but it was something like that where we needed to have
    //an extra aria attribute
    // https://github.com/evcohen/eslint-plugin-jsx-a11y/tree/master/docs/rules
    'jsx-a11y/anchor-has-content': 0,
    'jsx-a11y/href-no-hash': 0,
    'react/jsx-no-bind': [1, { ignoreRefs: true }]
  }
};
