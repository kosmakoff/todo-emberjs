window.Todos = Ember.Application.create();

// Todos.ApplicationAdapter = DS.FixtureAdapter.extend();

// Todos.ApplicationAdapter = DS.LSAdapter.extend({
//   namespace: 'todos-emberjs'
// });

Todos.ApplicationAdapter = DS.RESTAdapter.extend({
    host: 'https://todo-emberjs-kosmakoff.c9.io:5000',
    namespace: 'todos/api/v1.0'
});