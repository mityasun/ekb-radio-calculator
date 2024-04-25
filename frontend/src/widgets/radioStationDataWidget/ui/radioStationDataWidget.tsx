import clsx from 'clsx';
import s from './radioStationDataWidget.module.css';
import { DataWidget } from 'shared/ui/dataWidget';
import ReachDlyIcon from 'shared/assets/icon/people-group-svgrepo-com.svg?react';
import LocationIcon from 'shared/assets/icon/location-svgrepo-com.svg?react';
import GenderIcon from 'shared/assets/icon/man-and-woman-svgrepo-com.svg?react';
import AudienceAgeIcon from 'shared/assets/icon/time-management-svgrepo-com.svg?react';
import { useRadioStore } from 'shared/store';

export const RadioStationDataWidget = () => {
  const { selectedRadio } = useRadioStore();

  const data = [
    {
      title: 'охват аудитории (Reach Dly)',
      icon: <ReachDlyIcon />,
      value: [
        <>
          <h4>
            {selectedRadio?.reach_dly || '--'}
            <span> чел./сутки</span>
          </h4>
          <h4>
            {selectedRadio?.reach_dly_percent || '--'}
            <span> %</span>
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
          {selectedRadio?.broadcast_zone || '--'}
        </h4>
      ]
    },
    {
      title: 'пол аудитории',
      icon: <GenderIcon />,
      value: [
        <>
          <h4>
            <span>{selectedRadio?.audience_sex[1].sex || 'Женщины'} </span>
            {selectedRadio?.audience_sex[1].percent || '--'}
            <span>%</span>
          </h4>
          <h4>
            <span>{selectedRadio?.audience_sex[0].sex || 'Мужчины'} </span>
            {selectedRadio?.audience_sex[0].percent || '--'}
            <span>%</span>
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
            <span>ядро аудитории </span>
            {selectedRadio?.audience_sex[0].sex || '--'}
          </h4>
          <h4>
            {selectedRadio?.audience_sex[0].percent || '--'}
            <span> лет</span>
          </h4>
        </>
      ]
    }
  ];

  if (!selectedRadio) return null;

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
