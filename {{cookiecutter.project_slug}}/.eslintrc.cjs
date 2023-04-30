/* eslint-env node */
module.exports = {
  extends: [
    'plugin:vue/vue3-recommended',
    'eslint:recommended'
  ],
  overrides: [
    {
      files: ['*.js', '*.vue'],
    },
  ],
  rules: {
    'vue/multi-word-component-names': ['error', { ignores: ['Home'] }],
    'vue/html-self-closing': ['error', {
      'html': {
        'void': 'never',
        'normal': 'never',
        'component': 'never',
      }

    }]
  }
};
