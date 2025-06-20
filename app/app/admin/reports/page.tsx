
'use client';

import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { 
  BarChart3,
  Download,
  Calendar,
  DollarSign,
  TrendingUp,
  Users,
  Package,
  FileText
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
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  LineChart,
  Line
} from 'recharts';
import { formatCurrency } from '@/lib/utils';

// Mock data for charts
const salesData = [
  { month: 'Янв', revenue: 180000, orders: 12, profit: 54000 },
  { month: 'Фев', revenue: 220000, orders: 15, profit: 66000 },
  { month: 'Мар', revenue: 310000, orders: 20, profit: 93000 },
  { month: 'Апр', revenue: 290000, orders: 18, profit: 87000 },
  { month: 'Май', revenue: 340000, orders: 22, profit: 102000 },
  { month: 'Июн', revenue: 420000, orders: 28, profit: 126000 },
];

const projectTypeData = [
  { name: 'Кухни', value: 45, color: '#14B8A6' },
  { name: 'Детская мебель', value: 25, color: '#8B5CF6' },
  { name: 'Офисная мебель', value: 20, color: '#F59E0B' },
  { name: 'Спальни', value: 10, color: '#EF4444' },
];

const topMaterials = [
  { name: 'МДФ плита 18мм', usage: 85, cost: 157500 },
  { name: 'Фурнитура Blum', usage: 67, cost: 569500 },
  { name: 'Кромка ПВХ', usage: 92, cost: 41400 },
  { name: 'Столешница', usage: 34, cost: 238000 },
  { name: 'Лак полиуретановый', usage: 56, cost: 67200 },
];

const performanceMetrics = [
  { metric: 'Конверсия лидов', value: 68, target: 70, status: 'warning' },
  { metric: 'Средний чек', value: 285000, target: 300000, status: 'warning' },
  { metric: 'Время выполнения', value: 18, target: 21, status: 'good' },
  { metric: 'Повторные заказы', value: 34, target: 30, status: 'good' },
];

export default function ReportsPage() {
  const [dateRange, setDateRange] = useState('6months');
  const [reportType, setReportType] = useState('sales');

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
          <h1 className="text-2xl font-bold text-slate-900">Отчеты и аналитика</h1>
          <p className="text-slate-600">Анализ продаж, производительности и эффективности</p>
        </div>
        <div className="flex items-center space-x-3">
          <Select value={dateRange} onValueChange={setDateRange}>
            <SelectTrigger className="w-48">
              <SelectValue placeholder="Период" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="1month">Последний месяц</SelectItem>
              <SelectItem value="3months">Последние 3 месяца</SelectItem>
              <SelectItem value="6months">Последние 6 месяцев</SelectItem>
              <SelectItem value="1year">Последний год</SelectItem>
            </SelectContent>
          </Select>
          <Button variant="outline" size="sm">
            <Download className="h-4 w-4 mr-2" />
            Экспорт PDF
          </Button>
        </div>
      </motion.div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.1 }}
        >
          <Card>
            <CardContent className="p-4">
              <div className="flex items-center justify-between">
                <div>
                  <div className="text-2xl font-bold text-slate-900">
                    {formatCurrency(salesData.reduce((acc, item) => acc + item.revenue, 0))}
                  </div>
                  <p className="text-sm text-slate-600">Общая выручка</p>
                </div>
                <DollarSign className="h-8 w-8 text-green-500" />
              </div>
            </CardContent>
          </Card>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
        >
          <Card>
            <CardContent className="p-4">
              <div className="flex items-center justify-between">
                <div>
                  <div className="text-2xl font-bold text-slate-900">
                    {salesData.reduce((acc, item) => acc + item.orders, 0)}
                  </div>
                  <p className="text-sm text-slate-600">Общие заказы</p>
                </div>
                <Package className="h-8 w-8 text-blue-500" />
              </div>
            </CardContent>
          </Card>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.3 }}
        >
          <Card>
            <CardContent className="p-4">
              <div className="flex items-center justify-between">
                <div>
                  <div className="text-2xl font-bold text-slate-900">
                    {Math.round(salesData.reduce((acc, item) => acc + item.revenue, 0) / salesData.reduce((acc, item) => acc + item.orders, 0))}
                  </div>
                  <p className="text-sm text-slate-600">Средний чек</p>
                </div>
                <TrendingUp className="h-8 w-8 text-purple-500" />
              </div>
            </CardContent>
          </Card>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.4 }}
        >
          <Card>
            <CardContent className="p-4">
              <div className="flex items-center justify-between">
                <div>
                  <div className="text-2xl font-bold text-slate-900">68%</div>
                  <p className="text-sm text-slate-600">Конверсия лидов</p>
                </div>
                <Users className="h-8 w-8 text-orange-500" />
              </div>
            </CardContent>
          </Card>
        </motion.div>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Revenue Chart */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.5 }}
        >
          <Card>
            <CardHeader>
              <CardTitle>Выручка и заказы по месяцам</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="h-80">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={salesData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0" />
                    <XAxis 
                      dataKey="month" 
                      tick={{ fontSize: 12, fill: '#64748B' }}
                      tickLine={false}
                      stroke="#94A3B8"
                    />
                    <YAxis 
                      tick={{ fontSize: 12, fill: '#64748B' }}
                      tickLine={false}
                      stroke="#94A3B8"
                    />
                    <Tooltip 
                      formatter={(value, name) => [
                        name === 'revenue' ? formatCurrency(value as number) : value,
                        name === 'revenue' ? 'Выручка' : 'Заказы'
                      ]}
                      contentStyle={{
                        backgroundColor: '#FFFFFF',
                        border: '1px solid #E2E8F0',
                        borderRadius: '8px',
                        boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)'
                      }}
                    />
                    <Bar dataKey="revenue" fill="#14B8A6" radius={[4, 4, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </CardContent>
          </Card>
        </motion.div>

        {/* Project Types */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.6 }}
        >
          <Card>
            <CardHeader>
              <CardTitle>Распределение проектов по типам</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="h-80">
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie
                      data={projectTypeData}
                      cx="50%"
                      cy="50%"
                      innerRadius={60}
                      outerRadius={120}
                      paddingAngle={5}
                      dataKey="value"
                    >
                      {projectTypeData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.color} />
                      ))}
                    </Pie>
                    <Tooltip 
                      formatter={(value) => [`${value}%`, 'Доля']}
                      contentStyle={{
                        backgroundColor: '#FFFFFF',
                        border: '1px solid #E2E8F0',
                        borderRadius: '8px',
                        boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)'
                      }}
                    />
                  </PieChart>
                </ResponsiveContainer>
              </div>
              <div className="grid grid-cols-2 gap-2 mt-4">
                {projectTypeData.map((item) => (
                  <div key={item.name} className="flex items-center space-x-2">
                    <div 
                      className="w-3 h-3 rounded-full" 
                      style={{ backgroundColor: item.color }}
                    />
                    <span className="text-sm text-slate-600">{item.name}</span>
                    <span className="text-sm font-medium ml-auto">{item.value}%</span>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </motion.div>
      </div>

      {/* Performance Metrics */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.7 }}
      >
        <Card>
          <CardHeader>
            <CardTitle>Показатели эффективности</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              {performanceMetrics.map((metric, index) => (
                <div key={metric.metric} className="space-y-3">
                  <div className="flex items-center justify-between">
                    <h4 className="text-sm font-medium text-slate-900">{metric.metric}</h4>
                    <Badge variant={metric.status === 'good' ? 'default' : 'secondary'}>
                      {metric.status === 'good' ? 'Хорошо' : 'Внимание'}
                    </Badge>
                  </div>
                  <div className="text-2xl font-bold text-slate-900">
                    {typeof metric.value === 'number' && metric.value > 1000 
                      ? formatCurrency(metric.value)
                      : `${metric.value}${metric.metric.includes('Конверсия') || metric.metric.includes('Повторные') ? '%' : metric.metric.includes('Время') ? ' дней' : ''}`
                    }
                  </div>
                  <div className="text-sm text-slate-500">
                    Цель: {typeof metric.target === 'number' && metric.target > 1000 
                      ? formatCurrency(metric.target)
                      : `${metric.target}${metric.metric.includes('Конверсия') || metric.metric.includes('Повторные') ? '%' : metric.metric.includes('Время') ? ' дней' : ''}`
                    }
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </motion.div>

      {/* Top Materials */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.8 }}
      >
        <Card>
          <CardHeader>
            <CardTitle>Топ материалов по использованию</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {topMaterials.map((material, index) => (
                <div key={material.name} className="flex items-center justify-between p-3 rounded-lg hover:bg-slate-50">
                  <div className="flex items-center space-x-3">
                    <div className="w-8 h-8 bg-slate-100 rounded-lg flex items-center justify-center">
                      <span className="text-sm font-bold text-slate-600">{index + 1}</span>
                    </div>
                    <div>
                      <div className="font-medium text-slate-900">{material.name}</div>
                      <div className="text-sm text-slate-500">Использовано {material.usage}%</div>
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="font-medium text-slate-900">
                      {formatCurrency(material.cost)}
                    </div>
                    <div className="text-sm text-slate-500">затрачено</div>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </motion.div>

      {/* Quick Reports */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.9 }}
      >
        <Card>
          <CardHeader>
            <CardTitle>Быстрые отчеты</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <Button variant="outline" className="h-24 flex flex-col items-center justify-center space-y-2">
                <BarChart3 className="h-6 w-6" />
                <span className="text-sm">Отчет по продажам</span>
              </Button>
              <Button variant="outline" className="h-24 flex flex-col items-center justify-center space-y-2">
                <Users className="h-6 w-6" />
                <span className="text-sm">Анализ клиентов</span>
              </Button>
              <Button variant="outline" className="h-24 flex flex-col items-center justify-center space-y-2">
                <Package className="h-6 w-6" />
                <span className="text-sm">Отчет по складу</span>
              </Button>
              <Button variant="outline" className="h-24 flex flex-col items-center justify-center space-y-2">
                <FileText className="h-6 w-6" />
                <span className="text-sm">Финансовый отчет</span>
              </Button>
            </div>
          </CardContent>
        </Card>
      </motion.div>
    </div>
  );
}
