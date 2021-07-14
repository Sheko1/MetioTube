videojs('my-video', {
    playbackRates: [0.5, 1, 1.25, 1.5, 2, 3],
    plugins: {
        hotkeys: {
            enableModifiersForNumbers: false,
            enableVolumeScroll: false
        }
    }
})
