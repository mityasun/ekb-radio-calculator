export const getDaysInMonth = (month: number = 1) => {
  const currentMonth = new Date().getMonth() + 1;
  const year = currentMonth <= month ? new Date().getFullYear() : new Date().getFullYear() + 1;
  const date = new Date(year, month - 1, 1);
  const days = [];
  const daysOfWeek = ['ВС', 'ПН', 'ВТ', 'СР', 'ЧТ', 'ПТ', 'СБ'];

  while (date.getMonth() === month - 1) {
    const day = {
      date: date.getDate(),
      dayOfWeek: daysOfWeek[date.getDay()],
      isWeekend: [0, 6].includes(date.getDay())
    };
    days.push(day);
    date.setDate(date.getDate() + 1);
  }
  return days;
};
