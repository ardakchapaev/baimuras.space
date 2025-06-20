
'use client';

import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { 
  Calendar as CalendarIcon,
  Plus,
  Filter,
  Clock,
  MapPin,
  User,
  Phone,
  ChevronLeft,
  ChevronRight,
  CalendarDays
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { 
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { formatDateTime, getStatusColor, getStatusBadge } from '@/lib/utils';
import { Measurement } from '@/lib/types';

// Mock data
const mockMeasurements: Measurement[] = [
  {
    id: '1',
    title: 'Замер кухни у Ивановых',
    description: 'Замер для кухонного гарнитура',
    scheduledAt: new Date('2024-02-05T10:00:00'),
    duration: 90,
    status: 'scheduled',
    address: 'ул. Московская, 123, кв. 45',
    notes: 'Перезвонить за день до визита',
    userId: 'user1',
    createdAt: new Date('2024-01-20'),
    updatedAt: new Date('2024-01-20'),
    user: {
      id: 'user1',
      username: 'manager1',
      email: 'manager@baimuras.space',
      name: 'Менеджер',
      createdAt: new Date(),
      updatedAt: new Date(),
      roles: []
    }
  },
  {
    id: '2',
    title: 'Замер детской комнаты',
    description: 'Мебель Монтессори для ребенка',
    scheduledAt: new Date('2024-02-05T14:00:00'),
    duration: 60,
    status: 'scheduled',
    address: 'пр. Манаса, 67, кв. 12',
    notes: 'Есть домофон, код 1234',
    userId: 'user1',
    createdAt: new Date('2024-01-22'),
    updatedAt: new Date('2024-01-22'),
    user: {
      id: 'user1',
      username: 'manager1',
      email: 'manager@baimuras.space',
      name: 'Менеджер',
      createdAt: new Date(),
      updatedAt: new Date(),
      roles: []
    }
  },
  {
    id: '3',
    title: 'Замер офисного помещения',
    description: 'Рабочие места для IT-компании',
    scheduledAt: new Date('2024-02-06T11:00:00'),
    duration: 120,
    status: 'scheduled',
    address: 'БЦ "Орион", ул. Токтогула, 142, оф. 501',
    notes: 'Встреча с директором',
    userId: 'user1',
    createdAt: new Date('2024-01-25'),
    updatedAt: new Date('2024-01-25'),
    user: {
      id: 'user1',
      username: 'manager1',
      email: 'manager@baimuras.space',
      name: 'Менеджер',
      createdAt: new Date(),
      updatedAt: new Date(),
      roles: []
    }
  },
];

const daysOfWeek = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс'];
const months = [
  'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
  'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'
];

export default function CalendarPage() {
  const [measurements, setMeasurements] = useState<Measurement[]>(mockMeasurements);
  const [currentDate, setCurrentDate] = useState(new Date());
  const [viewMode, setViewMode] = useState<'month' | 'week' | 'day'>('month');
  const [statusFilter, setStatusFilter] = useState('all');

  const getDaysInMonth = (date: Date) => {
    const year = date.getFullYear();
    const month = date.getMonth();
    const firstDay = new Date(year, month, 1);
    const lastDay = new Date(year, month + 1, 0);
    const daysInMonth = lastDay.getDate();
    const startingDayOfWeek = (firstDay.getDay() + 6) % 7; // Convert to Monday = 0

    const days = [];
    
    // Add empty cells for days before the first day of the month
    for (let i = 0; i < startingDayOfWeek; i++) {
      days.push(null);
    }
    
    // Add days of the month
    for (let day = 1; day <= daysInMonth; day++) {
      days.push(new Date(year, month, day));
    }
    
    return days;
  };

  const getMeasurementsForDate = (date: Date | null) => {
    if (!date) return [];
    
    return measurements.filter(measurement => {
      const measurementDate = new Date(measurement.scheduledAt);
      return measurementDate.toDateString() === date.toDateString() &&
             (statusFilter === 'all' || measurement.status === statusFilter);
    });
  };

  const navigateMonth = (direction: 'prev' | 'next') => {
    setCurrentDate(prev => {
      const newDate = new Date(prev);
      newDate.setMonth(prev.getMonth() + (direction === 'next' ? 1 : -1));
      return newDate;
    });
  };

  const goToToday = () => {
    setCurrentDate(new Date());
  };

  const days = getDaysInMonth(currentDate);

  return (
    <div className="space-y-6">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="flex items-center justify-between"
      >
        <div>
          <h1 className="text-2xl font-bold text-slate-900">Календарь замеров</h1>
          <p className="text-slate-600">Планирование замеров и встреч с клиентами</p>
        </div>
        <div className="flex items-center space-x-3">
          <Button variant="outline" size="sm" onClick={goToToday}>
            <CalendarDays className="h-4 w-4 mr-2" />
            Сегодня
          </Button>
          <Button size="sm">
            <Plus className="h-4 w-4 mr-2" />
            Новый замер
          </Button>
        </div>
      </motion.div>

      {/* Calendar Controls */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.1 }}
      >
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-4">
                <div className="flex items-center space-x-2">
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => navigateMonth('prev')}
                  >
                    <ChevronLeft className="h-4 w-4" />
                  </Button>
                  <h2 className="text-xl font-semibold min-w-48 text-center">
                    {months[currentDate.getMonth()]} {currentDate.getFullYear()}
                  </h2>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => navigateMonth('next')}
                  >
                    <ChevronRight className="h-4 w-4" />
                  </Button>
                </div>
              </div>
              
              <div className="flex items-center space-x-3">
                <Select value={statusFilter} onValueChange={setStatusFilter}>
                  <SelectTrigger className="w-48">
                    <SelectValue placeholder="Статус" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">Все статусы</SelectItem>
                    <SelectItem value="scheduled">Запланированы</SelectItem>
                    <SelectItem value="completed">Завершены</SelectItem>
                    <SelectItem value="cancelled">Отменены</SelectItem>
                    <SelectItem value="rescheduled">Перенесены</SelectItem>
                  </SelectContent>
                </Select>
                
                <Select value={viewMode} onValueChange={(value: any) => setViewMode(value)}>
                  <SelectTrigger className="w-32">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="month">Месяц</SelectItem>
                    <SelectItem value="week">Неделя</SelectItem>
                    <SelectItem value="day">День</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>
          </CardContent>
        </Card>
      </motion.div>

      {/* Calendar Grid */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.2 }}
      >
        <Card>
          <CardContent className="p-6">
            {/* Days of week header */}
            <div className="grid grid-cols-7 gap-1 mb-4">
              {daysOfWeek.map((day) => (
                <div
                  key={day}
                  className="p-3 text-center text-sm font-medium text-slate-600 border-b"
                >
                  {day}
                </div>
              ))}
            </div>
            
            {/* Calendar days */}
            <div className="grid grid-cols-7 gap-1">
              {days.map((date, index) => {
                const measurementsForDate = getMeasurementsForDate(date);
                const isToday = date && date.toDateString() === new Date().toDateString();
                const isCurrentMonth = date && date.getMonth() === currentDate.getMonth();
                
                return (
                  <div
                    key={index}
                    className={`min-h-24 p-2 border border-slate-100 ${
                      !date ? 'bg-slate-50' : 
                      isToday ? 'bg-teal-50 border-teal-200' :
                      !isCurrentMonth ? 'text-slate-400' : 'hover:bg-slate-50'
                    } transition-colors`}
                  >
                    {date && (
                      <>
                        <div className={`text-sm font-medium mb-1 ${
                          isToday ? 'text-teal-600' : 'text-slate-900'
                        }`}>
                          {date.getDate()}
                        </div>
                        
                        <div className="space-y-1">
                          {measurementsForDate.slice(0, 2).map((measurement) => (
                            <div
                              key={measurement.id}
                              className={`p-1 rounded text-xs cursor-pointer ${getStatusColor(measurement.status)}`}
                              title={`${measurement.title} - ${formatDateTime(measurement.scheduledAt)}`}
                            >
                              <div className="flex items-center space-x-1">
                                <Clock className="h-3 w-3" />
                                <span className="truncate">
                                  {new Date(measurement.scheduledAt).toLocaleTimeString('ru-RU', { 
                                    hour: '2-digit', 
                                    minute: '2-digit' 
                                  })}
                                </span>
                              </div>
                              <div className="truncate font-medium">
                                {measurement.title}
                              </div>
                            </div>
                          ))}
                          
                          {measurementsForDate.length > 2 && (
                            <div className="text-xs text-slate-500 p-1">
                              +{measurementsForDate.length - 2} еще
                            </div>
                          )}
                        </div>
                      </>
                    )}
                  </div>
                );
              })}
            </div>
          </CardContent>
        </Card>
      </motion.div>

      {/* Today's Schedule */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.3 }}
      >
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <CalendarIcon className="h-5 w-5 text-teal-500" />
              <span>Сегодняшние замеры</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {getMeasurementsForDate(new Date()).length === 0 ? (
                <div className="text-center py-8">
                  <CalendarIcon className="h-12 w-12 text-slate-300 mx-auto mb-3" />
                  <p className="text-slate-500">Нет запланированных замеров на сегодня</p>
                </div>
              ) : (
                getMeasurementsForDate(new Date()).map((measurement) => (
                  <div
                    key={measurement.id}
                    className="flex items-start space-x-4 p-4 rounded-lg border hover:bg-slate-50 transition-colors"
                  >
                    <div className="w-16 text-center">
                      <div className="text-sm font-medium text-slate-900">
                        {new Date(measurement.scheduledAt).toLocaleTimeString('ru-RU', { 
                          hour: '2-digit', 
                          minute: '2-digit' 
                        })}
                      </div>
                      <div className="text-xs text-slate-500">
                        {measurement.duration} мин
                      </div>
                    </div>
                    
                    <div className="flex-1">
                      <div className="flex items-center justify-between mb-2">
                        <h4 className="font-medium text-slate-900">
                          {measurement.title}
                        </h4>
                        <Badge className={getStatusColor(measurement.status)}>
                          {getStatusBadge(measurement.status)}
                        </Badge>
                      </div>
                      
                      <p className="text-sm text-slate-600 mb-2">
                        {measurement.description}
                      </p>
                      
                      {measurement.address && (
                        <div className="flex items-center text-sm text-slate-500 mb-1">
                          <MapPin className="h-4 w-4 mr-1" />
                          {measurement.address}
                        </div>
                      )}
                      
                      <div className="flex items-center text-sm text-slate-500">
                        <User className="h-4 w-4 mr-1" />
                        {measurement.user.username}
                      </div>
                      
                      {measurement.notes && (
                        <div className="mt-2 p-2 bg-amber-50 rounded text-sm text-amber-800">
                          <strong>Заметка:</strong> {measurement.notes}
                        </div>
                      )}
                    </div>
                    
                    <div className="flex flex-col space-y-2">
                      <Button variant="outline" size="sm">
                        <Phone className="h-4 w-4" />
                      </Button>
                      <Button variant="outline" size="sm">
                        <MapPin className="h-4 w-4" />
                      </Button>
                    </div>
                  </div>
                ))
              )}
            </div>
          </CardContent>
        </Card>
      </motion.div>
    </div>
  );
}
