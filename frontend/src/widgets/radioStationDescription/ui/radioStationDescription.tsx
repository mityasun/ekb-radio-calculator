/* eslint-disable max-len */
import clsx from 'clsx';
import s from './radioStationDescription.module.css';

const logoLink = 'https://upload.wikimedia.org/wikipedia/ru/archive/3/31/20071213132033%21Avtoradio.png';
const logoImgAlt = 'Логотип радиостанции';
const descriptionText = [
  '«Авторадио» – одна из первых в России коммерческих радиостанций, ведет свою историю с мая 1993 года.',
  '«Авторадио» с большим отрывом лидирует по всей России среди автомобильной аудитории, полностью оправдывая звание Первого автомобильного радио.',
  '«Авторадио» – это лучшее утреннее шоу страны, неоднократный лауреат «Радиомании».',
  '«Авторадио» – это надежная и оперативная информация о пробках.',
  '«Авторадио» – это постоянно идущие в эфире игры и розыгрыши призов, это яркие массовые акции.',
  'И в первую очередь международный фестиваль «Дискотека 80-х», ежегодно собирающий десятки тысяч поклонников в Москве, Санкт-Петербурге, Екатеринбурге и других городах.'
];
const city = 'Екатеринбург';
const radioStation = 'Авторадио';

const DescriptionTitle = `Размещение рекламы на ${radioStation} в городе ${city}`;

export const RadioStationDescription = () => {
  return (
    <div className={clsx(s.radioStationDescription)}>
      <div className={clsx(s.radioStationLogo)}>
        <img src={logoLink} alt={logoImgAlt} />
      </div>
      <div className={clsx(s.radioStationDescriptionText)}>
        <h3>{DescriptionTitle}</h3>
        <article>
          {descriptionText.map((text, index) => (
            <p key={index}>{text}</p>
          ))}
        </article>
      </div>
    </div>
  );
};
