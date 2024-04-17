import clsx from 'clsx';
import s from './radioStationDataWidget.module.css';
import { DataWidget } from 'shared/ui/dataWidget';
import ReachDlyIcon from 'shared/assets/icon/people-group-svgrepo-com.svg?react';
import LocationIcon from 'shared/assets/icon/location-svgrepo-com.svg?react';
import GenderIcon from 'shared/assets/icon/man-and-woman-svgrepo-com.svg?react';
import AudienceAgeIcon from 'shared/assets/icon/time-management-svgrepo-com.svg?react';

const data = [
  {
    title: 'охват аудитории',
    icon: <ReachDlyIcon />,
    value: [
      <>
        <h4>
          1236555<span> тыс.чел.</span>
        </h4>
        <h4>
          5<span> %</span>
        </h4>
      </>
    ]
  },
  {
    title: 'зона вещания',
    icon: <LocationIcon />,
    value: [
      <h4>
        <br />
        Екатеринбург
      </h4>
    ]
  },
  {
    title: 'пол аудитории',
    icon: <GenderIcon />,
    value: [
      <>
        <h4>
          <span>мужчины </span>45<span>%</span>
        </h4>
        <h4>
          <span>женщины </span>55<span>%</span>
        </h4>
      </>
    ]
  },
  {
    title: 'возраст аудитории',
    icon: <AudienceAgeIcon />,
    value: [
      <>
        <h4>
          <span>ядро аудитории </span>44<span>%</span>
        </h4>
        <h4>
          30-49<span>% лет</span>
        </h4>
      </>
    ]
  }
];

export const RadioStationDataWidget = () => {
  return (
    <div className={clsx(s.radioStationDataWidget)}>
      {data.map((item, index) => (
        <DataWidget key={index} title={item.title} icon={item.icon}>
          {item.value.map((text, index) => (
            <div key={index}>{text}</div>
          ))}
        </DataWidget>
      ))}
    </div>
  );
};
