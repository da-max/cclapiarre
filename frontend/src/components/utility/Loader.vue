<template>
    <div class="uk-overlay uk-overlay-primary uk-position-cover" id="loader">
            <div class="uk-position-center uk-position-fixed uk-text-bold uk-text-warning uk-h3">
                    <span uk-spinner="ratio: 5"></span> Chargement en cours
            </div>
        </div>
</template>

<script>
export default {
    name: "Loader"
}
</script>