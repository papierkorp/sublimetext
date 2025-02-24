module.exports = {
  env: {
    browser: true,
    node: true,
  },
  extends: [
    // By extending from a plugin config, we can get recommended rules without having to add them manually.
    'eslint:recommended',
    'plugin:react/recommended',
    'plugin:import/recommended',
    'plugin:jsx-a11y/recommended',
    'plugin:@typescript-eslint/recommended',
    'plugin:react/jsx-runtime',
    // This disables the formatting rules in ESLint that Prettier is going to be responsible for handling.
    // Make sure it's always the last config, so it gets the chance to override other configs.
    'eslint-config-prettier',
  ],
  settings: {
    react: {
      // Tells eslint-plugin-react to automatically detect the version of React to use.
      version: 'detect',
    },
    // Tells eslint how to resolve imports
    'import/resolver': {
      node: {
        paths: ['src'],
        extensions: ['.js', '.jsx', '.ts', '.tsx'],
      },
    },
  },
  rules: {
    // Add your own rules here to override ones from the extended configs.

    //TODO:
    // stage 2: https://jira.sirconic-group.de/browse/LEASTWO-1204
    // stage 3: https://jira.sirconic-group.de/browse/LEASTWO-1214

    '@typescript-eslint/no-unused-vars': 2,
    'no-trailing-spaces': 'error',
    'no-nested-ternary': 'warn',
    '@typescript-eslint/ban-ts-comment': 1,
  },
};