import {themes as prismThemes} from 'prism-react-renderer';

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Brew',
  favicon: 'img/favicon.ico',

  url: 'https://appbrew.netfily.app',
  baseUrl: '/',

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',


  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: './sidebars.js',
          routeBasePath: '/',
          editUrl:
            'https://github.com/brew-foundation/brew/tree/main/website',
        },
        blog: {
          showReadingTime: true,
          editUrl:
            'https://github.com/facebook/docusaurus/tree/main/packages/create-docusaurus/templates/shared/',
        },
        theme: {
          customCss: './src/css/custom.css',
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      // Replace with your project's social card
      image: 'img/docusaurus-social-card.jpg',
      navbar: {
        title: 'Brew',
        logo: {
          alt: 'Brew Logo',
          src: 'img/logo.svg',
        },
        items: [
          {
            type: 'docSidebar',
            sidebarId: 'docSidebar',
            position: 'left',
            label: 'Pages 📃',
          },
          {
          type: 'dropdown',
          label: 'Community ✨',
          position: 'right',
          items: [
            {
            type: 'docSidebar',
            sidebarId: 'communitySidebar',
            label: 'Community ✨',
            },
            {
            type: 'docSidebar',
            sidebarId: 'devSidebar',
            label: 'Developers 💻',
            },
            {
              label: 'brew-api 📦',
              href: 'https://www.github.com/brew-foundation/brew-api',
            },
          ],
        },
          {to: '/blog', label: 'Blog 📜', position: 'left'},
          {
            type: 'docSidebar',
            sidebarId: 'legalSidebar',
            position: 'right',
            label: 'Legal 🔨',
          },
          {
            href: 'https://github.com/brew-foundation/brew',
            label: 'GitHub',
            position: 'right',
          },
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Brew',
            items: [
              {
                label: 'Home',
                to: '/',
              },
              {
                label: 'Developers',
                to: '/developers/',
              },
              {
                label: 'Community',
                to: '/community/',
              },
            ],
          },
          {
            title: 'Community',
            items: [
              {
                label: 'GitHub Organization',
                href: 'https://github.com/brew-foundation',
              },
            ],
          },
          {
            title: 'More',
            items: [
              {
                label: 'Blog',
                to: '/blog',
              },
              {
                html: `
                    <a href="https://www.netlify.com" target="_blank" rel="noreferrer noopener" aria-label="Deploys by Netlify">
                      <img src="https://www.netlify.com/img/global/badges/netlify-color-accent.svg" alt="Deploys by Netlify" width="114" height="51" />
                    </a>
                  `,
              },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} Brew Foundation. Built with Docusaurus.`,
      },
      colorMode: {
        defaultMode: 'dark',
        disableSwitch: true,
        respectPrefersColorScheme: false,
      },
      prism: {
        theme: prismThemes.github,
        darkTheme: prismThemes.dracula,
      },
    }),
};

export default config;
