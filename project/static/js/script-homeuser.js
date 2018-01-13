function mediaFragOne() {
    var video, sources, nav, buttons;
    video = document.querySelector('video#frag1');
    sources = video.getElementsByTagName('source');
    nav = document.querySelector('video#frag1+nav');
    buttons = nav.getElementsByTagName('button');

    for (var i = buttons.length - 1; i >= 0; i--) {
        buttons[i].addEventListener('click', function() {
            for (var i = sources.length - 1; i >= 0; i--) {
                sources[i].setAttribute(
                    'src', (sources[i].getAttribute('data-original')
                    .concat('#t=' + this.getAttribute('data-start'))));
                    video.load();
                    video.play();
            };
        });
    }
}
mediaFragOne();