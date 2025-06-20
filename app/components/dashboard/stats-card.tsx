
'use client';

import React from 'react';
import { motion } from 'framer-motion';
import { LucideIcon, TrendingUp, TrendingDown } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';
import { cn } from '@/lib/utils';

interface StatsCardProps {
  title: string;
  value: string | number;
  change?: number;
  changeLabel?: string;
  icon: LucideIcon;
  color?: 'blue' | 'green' | 'purple' | 'orange';
  index?: number;
}

export function StatsCard({ 
  title, 
  value, 
  change, 
  changeLabel, 
  icon: Icon, 
  color = 'blue',
  index = 0 
}: StatsCardProps) {
  const colorClasses = {
    blue: 'bg-blue-500',
    green: 'bg-green-500',
    purple: 'bg-purple-500',
    orange: 'bg-orange-500',
  };

  const isPositiveChange = change !== undefined && change > 0;
  const isNegativeChange = change !== undefined && change < 0;

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: index * 0.1 }}
    >
      <Card className="bg-white border-0 shadow-lg hover:shadow-xl transition-all duration-300">
        <CardContent className="p-6">
          <div className="flex items-center justify-between">
            <div className="flex-1">
              <p className="text-sm font-medium text-slate-600 mb-1">{title}</p>
              <p className="text-2xl font-bold text-slate-900 mb-2">{value}</p>
              
              {change !== undefined && (
                <div className="flex items-center space-x-1">
                  {isPositiveChange && (
                    <TrendingUp className="h-4 w-4 text-green-500" />
                  )}
                  {isNegativeChange && (
                    <TrendingDown className="h-4 w-4 text-red-500" />
                  )}
                  <span className={cn(
                    'text-sm font-medium',
                    isPositiveChange && 'text-green-600',
                    isNegativeChange && 'text-red-600',
                    !isPositiveChange && !isNegativeChange && 'text-slate-500'
                  )}>
                    {change > 0 && '+'}
                    {change.toFixed(1)}%
                  </span>
                  {changeLabel && (
                    <span className="text-sm text-slate-500">{changeLabel}</span>
                  )}
                </div>
              )}
            </div>
            
            <div className={cn(
              'w-12 h-12 rounded-xl flex items-center justify-center',
              colorClasses[color]
            )}>
              <Icon className="h-6 w-6 text-white" />
            </div>
          </div>
        </CardContent>
      </Card>
    </motion.div>
  );
}
