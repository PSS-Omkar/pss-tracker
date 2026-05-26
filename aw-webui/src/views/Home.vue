<template lang="pug">
div
  b-alert(v-if="$isAndroid" show)
    | #[b Note:] pss-tracker on Android is in a very early stage of development. There will be bugs, but we hope you bear with us as we refine things and get it on par with the desktop version of pss-tracker (which you should try!).

  h3 Welcome,
  p
    | Welcome to the PSS Tracker Dashboard! We're glad to have you on board.
    | PSS Tracker helps you stay productive and analyze your daily habits.
  p
    | If you are a developer, we hope you can contribute by writing a watcher, visualization, or something else on GitHub!
  p
    div Thank you for using PSS Tracker!
    small If you have a minute to spare, please check out the #[a(href="https://github.com/PSS-Omkar/psstracker/issues") Issue Tracker] to request new features.

  hr

  div.row
    div.col-md-6
      h4 Spread the word
      p
        | Nothing is as motivating as getting PSS Tracker into the hands of users.
        | By sharing it you get us to make PSS Tracker even better!
      ul
        li Star us on #[a(href="https://github.com/PSS-Omkar/psstracker") GitHub]
        li Report issues on the #[a(href="https://github.com/PSS-Omkar/psstracker/issues") Issue Tracker]

    div.col-md-6
      h4 Support us!
      p
        | Do you like PSS Tracker? Help us by contributing to the codebase on GitHub.

  hr

  div.row
    div.col-md-6
      h4 Resources
      p
        ul
          li #[a(href="https://psstracker.phylon.in/") Dashboard]
          li #[a(href="https://github.com/PSS-Omkar/psstracker") Source Code]
          li #[a(href="/api/") API Browser]

    div.col-md-6
      h4 Documentation
      p
        | Check out our #[a(href="https://github.com/PSS-Omkar/psstracker/blob/main/README.md") official documentation]!

  hr

  p
    small
      i
        | You can change which page opens when you open pss-tracker (instead of this page) in the #[router-link(to="/settings") settings].

</template>

<script lang="ts">
export default {
  name: 'Home',
};
</script>
