import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import en from './locales/en.json';
import hi from './locales/hi.json';

export const SUPPORTED_LANGS = ['en', 'hi'] as const;
export type Lang = (typeof SUPPORTED_LANGS)[number];

const stored = (typeof window !== 'undefined' ? localStorage.getItem('igot_lang') : null) as Lang | null;
const initialLang: Lang = stored === 'hi' ? 'hi' : 'en';

i18n.use(initReactI18next).init({
  resources: {
    en: { translation: en },
    hi: { translation: hi },
  },
  lng: initialLang,
  fallbackLng: 'en',
  interpolation: { escapeValue: false },
  returnNull: false,
});

export const getCurrentLang = (): Lang => (i18n.language === 'hi' ? 'hi' : 'en');

export const setLanguage = (lang: Lang) => {
  localStorage.setItem('igot_lang', lang);
  document.documentElement.lang = lang === 'hi' ? 'hi' : 'en';
  i18n.changeLanguage(lang);
};

document.documentElement.lang = initialLang === 'hi' ? 'hi' : 'en';

export default i18n;
