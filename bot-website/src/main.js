import App from './App.svelte';
import { mount } from "svelte";

const app = mount(App, {
	target: document.body,
	props: {
		utilities: '<li>weather <city> - get a 5-day forecast in a specified city</li><li>timein (or ti) <city> - find the time in a city</li><li>pollhelp - view commands for making a poll</li>',
		minigames:'<li>scramble - unscramble a word and win points!</li><li>trivia - get a trivia question and win points!</li><li>leaderboard - view the server\'s leaderboard</li>',
		other: '<li>fact - get a random fact!</li>'
	}
});

export default app;