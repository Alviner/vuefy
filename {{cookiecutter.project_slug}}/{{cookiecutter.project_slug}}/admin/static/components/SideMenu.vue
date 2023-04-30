<template id="side-menu">
	<div class="side-menu">
		<router-link
			to="/"
			class="side-menu__logo"
			aria-label="Admin"
		></router-link>
	</div>
</template>

<script>
export default {
	template: '#side-menu',
};
</script>


<style>
.side-menu {
	flex-shrink: 0;
	width: 72px;
	background-color: #2E384D;
}

.side-menu a {
	display: flex;
	margin: auto;
}

.side-menu a + a {
	margin-top: 16px;
}

.side-menu__logo {
	background-image: url('/static/assets/logo.svg');
	height: 60px;
}

.side-menu__icon {
	width: 48px;
	height: 48px;
	align-items: center;
	justify-content: center;
	border-radius: 8px;
	transition-duration: 0.2s;
	transition-property: background-color;
}

.side-menu__icon:hover,
.side-menu__icon.router-link-active {
	background-color: #3D4C66;
}
</style>
