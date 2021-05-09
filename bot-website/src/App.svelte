<script>
	export let name;
	export let utilities;
	export let minigames;
</script>

<main>
	<div class = 'header'>
		<h1 class = 'h1-header'><strong>JuliaBot Discord Bot</strong></h1>	
	</div>
	<div class = 'content'>
		<div class = 'add-bot'>
			<a href = 'https://discord.com/api/oauth2/authorize?client_id=788643876876976139&permissions=3691510896&scope=bot' target='_blank'>
				<img src = 'https://upload.wikimedia.org/wikipedia/commons/thumb/f/f3/Eo_circle_pink_letter-j.svg/768px-Eo_circle_pink_letter-j.svg.png' alt = 'discord logo' class = 'discord-logo'>
			</a>
			<h2>Add this bot!</h2>
		</div>
		<div class = 'info'>
			<div id= 'about'>
				<h1>About</h1>	
				<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</p>
			</div>
			<div id= 'features'>
				<h1>Features</h1>
				<p><strong>Command syntax: !j &lt;command name&gt;</strong></p>
				<div class = 'list'>
					<h2>Utility commands</h2>
					<ul>
						{@html utilities}	
					</ul>
					<h2>Minigames</h2>
					<ul>
						{@html minigames}	
					</ul>
				</div>
			</div>
		</div>
	</div>
</main>

<style>
	main {
		text-align: center;
		margin: 0 auto;
		background-color: #d19e9e; 
	}

	h1 {
		color: #8a3b3b;
		text-transform: uppercase;
		font-size: 4em;
		font-weight: 100;
		margin: 0 auto;
	}

	h2 {
		color: #965d5d
	}


	@media (min-width: 640px) {
		main {
			max-width: none;
		}
	}

	.header {
		height: 100px;
		margin: 0 auto;
	}

	.h1-header {
		margin: 0 auto;
		padding: 5px;
	}

	.content {
		text-align:left;
		padding: 30px 200px 30px;
		background-color: #edd1d1;
		overflow: hidden;	
	}

	.info {
		margin: 0 auto;
		border-left: 3px solid #965d5d;
		border-right: 3px solid #965d5d;
		padding-left: 50px;
		padding-right: 50px;
		padding-top: 10px;
		padding-bottom: 10px;
		float:right;
		width: 50%;
	}

	.discord-logo {
		border-radius: 50%;
		width: 200px;
		height: 200px;
		object-fit: cover;
		background-color: #f1b3b3;
	}

	.discord-logo:hover {
		border: 4px solid #6b2e2e;
		border-style: dashed;
	}

	.add-bot {
		text-align: center;
		float:left;
		padding-left: 50px;
		padding-top:25vh;
	}
	

</style>