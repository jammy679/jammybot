import App from './App.svelte';

const app = new App({
	target: document.body,
	props: {
		name: 'world',
		utilities: '<li>timein (or ti) <city> - find the time in a city</li><li>pollhelp - view commands for making a poll</li>',
		minigames:'<li>fact - get a random fact!</li><li>scramble - unscramble a word and win points!</li><li>trivia - get a trivia question and win points!</li>'
	}
});

export default app;